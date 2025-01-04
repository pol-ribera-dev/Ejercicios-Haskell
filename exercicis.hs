fizzBuzz :: [Either Int String]
fizzBuzz = map calcula [0..]

calcula::Int-> Either Int String
calcula n  
    |mod n 15 == 0 = Right "FizzBuzz"
    |mod n 3 == 0 = Right "Fizz"
    |mod n 5 == 0 = Right "Buzz"
    |otherwise = Left n 


myLength :: [Int] -> Int
myLength [] = 0
myLength (_:xs) = 1 + myLength xs

insert :: [Int] -> Int -> [Int] 
insert [] x = [x] 
insert (y:z) x  
	| y >= x = x : y :z
	| True = y: insert z x

myIterate :: (a -> a) -> a -> [a]
myIterate f x = x : myIterate f (f x)

myFoldl :: (a -> b -> a) -> a -> [b] -> a
myFoldl _ acc [] = acc
myFoldl f x (y:z) = myFoldl f (f x y) z 


lookNsay :: [Integer]
lookNsay = map read (iterate sig "1") 

sig :: [Char] -> [Char]
sig [] = []
sig x = show (length ( takeWhile (== head x) x)) ++ [head x] ++ sig (dropWhile (== head x ) x)


eql :: [Int] -> [Int] -> Bool

eql a b 
    | length a /= length b = False
    | True  = foldl (&&) True (zipWith (==) a b) 

prod :: [Int] -> Int
prod a = foldl (*) 1 a

myFilter :: (a -> Bool) -> [a] -> [a]
myFilter f n = [x| x<-n, f x]


instance Functor (Queue) where
 fmap f (Queue x y) = Queue (fmap f x) (fmap f y)

data Queue a = Queue [a] [a]
    deriving (Show)

create :: Queue a 
create = Queue [][]
 
push :: a -> Queue a -> Queue a
push x (Queue l r) = Queue l (x:r)

pop :: Queue a -> Queue a
pop (Queue [][]) = Queue [][]
pop (Queue [] rs) = pop $ Queue (reverse rs) []
pop (Queue (x:xs) rs) = Queue xs rs

top :: Queue a -> a
top (Queue (x:xs) _) = x
top (Queue [] x) = top $ Queue (reverse x) []

empty :: Queue a -> Bool
empty (Queue [][]) = True
empty (Queue _ _) = False

translation :: Num b => b -> Queue b -> Queue b
translation a (Queue x y) = fmap (+a) (Queue x y) 





calcul :: Int -> Int -> Char -> Either String Int
calcul x y '+' = Right (x+y)
calcul x y '*' = Right (x*y)
calcul x y '-'
    | x < y = Left "neg"
    | True = Right (x-y)
calcul x 0 '/' = Left "div0"
calcul x y '/'
    | (mod x y) == 0 = Left "divE"
    | True = Right (div x y)

--main::IO()
--main = do
--    input<-getLine
--    let result = foldl (calcul) 0 input
--    putStrLn result
--    main


data Tree a = Empty | Node a (Tree a) (Tree a)

instance (Show a) => Show (Tree a) where
	show Empty = "()"
	show (Node value l r) = "(" ++ show l ++ "," ++ show value ++ "," ++ show r++ ")" 

instance Functor Tree where
    fmap f Empty = Empty
    fmap f (Node a l r) = Node (f a) (fmap f l) (fmap f r)

doubleT :: Num a => Tree a -> Tree a
doubleT a = fmap (*2) a