#Description of the function: IT takes two inputs (a dataframe of tweets, and a search string) 
#The script does the following:
#1) subsets the inputted dataset to contain only tweets with the specified search term, 
#2) performs a sentiment analysis on tweets that contain the inputted search term,
#3) plots a histogram of the sentiment scores, and 4) returns the sentiment scores as output.  
#Plot the resulting sentiment scores in a side-by-side boxplot.  


# Ensure Package loads a package, and installs it first if necessary
EnsurePackage<-function(x){
  x <- as.character(x)
  if (!require(x,character.only=TRUE)){
    install.packages(pkgs=x,
                     repos="http://cran.r-project.org")
    require(x,character.only=TRUE)}
}

EnsurePackage("stringr")
A8<-d
PrepareTwitter()
score.sentiment = function(sentences, pos.words, neg.words, .progress='none')
  library(string

CARword <- function(tweets,hashtag) {
  subset.CARword <- tweets[str_detect(tweets$text, hashtag),]
  subset2<- subset.CARword$text
  final.score <- score.sentiment(subset2, pos.words, neg.words)
  hist(final.score$score)
  print(final.score)
}

CARword(A8,"ford")

red <- CARword(A8,"ford")
blue <- CARword(A8,"revenue")

par (mfrow=c(1,2))
boxplot(Red, Blue, names=c("ford","revenue"),YLAB="SENTIMENT")

new=A8[-11,]

