{-# LANGUAGE OverloadedStrings, GeneralizedNewtypeDeriving #-}
-- An example of embedding a custom monad into
-- Scotty's transformer stack, using ReaderT to provide access
-- to a TVar containing global state.
--
-- Note: this example is somewhat simple, as our top level
-- is IO itself. The types of 'scottyT' and 'scottyAppT' are
-- general enough to allow a Scotty application to be
-- embedded into any MonadIO monad.
module Main (main) where

import Control.Applicative
import Control.Concurrent.STM
import Control.Monad.Reader
import Debug.Trace
import Network.HTTP.Types (status404)

import System.Environment
import Data.Default.Class
import Data.String
import Data.List ((\\), intersect)
import Data.Text.Lazy (Text, inits, pack)
import qualified Data.Map as M

import Network.Wai.Middleware.RequestLogger

import Prelude

import Web.Scotty.Trans

data DHT = DHT { dht     :: M.Map Text Text 
               , slots   :: [Text]
               , key     :: Text }

lookupDHT :: Text -> DHT -> Maybe Text
lookupDHT k = M.lookup k . dht

createDHT :: Text -> DHT
createDHT k = DHT M.empty (inits k) k

insertDHTslots :: [Text] -> Text -> Text -> DHT -> DHT
insertDHTslots []     _ _ d = d
insertDHTslots (s:ss) k v d = trace ("Trying to add " ++ show k ++ " in the slot " ++ show s ++ " slots -> " ++ show ss) $
    d { dht = M.insert k v (dht d), slots = slots d \\ [s] }

insertDHT :: Text -> Text -> DHT -> DHT
insertDHT k v d = case M.lookup k (dht d) of
    Nothing -> insertDHTslots (reverse cks) k v d
    Just _  -> d
  where cks = intersect (inits k) (slots d) 

-- Why 'ReaderT (TVar AppState)' rather than 'StateT AppState'?
-- With a state transformer, 'runActionToIO' (below) would have
-- to provide the state to _every action_, and save the resulting
-- state, using an MVar. This means actions would be blocking,
-- effectively meaning only one request could be serviced at a time.
-- The 'ReaderT' solution means only actions that actually modify
-- the state need to block/retry.
--
-- Also note: your monad must be an instance of 'MonadIO' for
-- Scotty to use it.
newtype WebM a = WebM { runWebM :: ReaderT (TVar DHT) IO a }
    deriving (Applicative, Functor, Monad, MonadIO, MonadReader (TVar DHT))

-- Scotty's monads are layered on top of our custom monad.
-- We define this synonym for lift in order to be explicit
-- about when we are operating at the 'WebM' layer.
webM :: MonadTrans t => WebM a -> t WebM a
webM = lift

-- Some helpers to make this feel more like a state monad.
gets :: (DHT -> b) -> WebM b
gets f = ask >>= liftIO . readTVarIO >>= return . f

modify :: (DHT -> DHT) -> WebM ()
modify f = ask >>= liftIO . atomically . flip modifyTVar' f

main :: IO ()
main = do
    [key] <- getArgs
    sync <- newTVarIO (createDHT $ pack key)
        -- 'runActionToIO' is called once per action.
    let runActionToIO m = runReaderT (runWebM m) sync

    scottyT 3000 runActionToIO app

-- This app doesn't use raise/rescue, so the exception
-- type is ambiguous. We can fix it by putting a type
-- annotation just about anywhere. In this case, we'll
-- just do it on the entire app.
app :: ScottyT Text WebM ()
app = do
    middleware logStdoutDev
    get "/" $ do
        c <- webM $ gets dht
        text $ fromString $ show c

    get "/insert/:key/:value" $ do
        k <- param "key"
        v <- param "value"
        webM $ modify $ \ st -> insertDHT k v st
        redirect "/"

    get "/lookup/:key" $ do
        k <- param "key"
        c <- webM $ gets $ lookupDHT k
        case c of
          Nothing -> status status404
          Just x -> text $ fromString $ show c
