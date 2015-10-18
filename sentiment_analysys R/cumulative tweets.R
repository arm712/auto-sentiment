rm(list=ls())

setwd("/Users/huyenle/Documents/School work/Fall 2013/QAC211_Data primer/Wesleyan")

write.csv(CTweets, file="tweets_10_17.csv", sep=",",row.names=F)
tweet1 <- read.csv("tweets_9_22.csv")
tweet2 <- read.csv("tweets_10_13.csv")
tweet3<-read.csv("tweets_10_13.csv")

tweet.updated <- rbind(tweet1,tweet2,tweet3)

d <- tweet.updated
