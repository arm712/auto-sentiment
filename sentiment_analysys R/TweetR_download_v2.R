
# Needed for the PrepareTwitter function
# Simply for convenience, packages can be installed and loaded on their own
EnsurePackage<-function(x)
{
  x <- as.character(x)
  if (!require(x,character.only=TRUE))
  {
    install.packages(pkgs=x,repos="http://cran.r-project.org")
    require(x,character.only=TRUE)
  }
}
# Create A Function to Load Dependencies
PrepareTwitter<-function()
{
  EnsurePackage("bitops")
  EnsurePackage("RCurl")
  EnsurePackage("RJSONIO")
  EnsurePackage("twitteR")
  EnsurePackage("ROAuth")
}
#Load Packages -- Just have to run this line next time downloading twits
PrepareTwitter()

#Authentication
credential <- OAuthFactory$new(consumerKey="pRoNAtephzJVgRFJuqUAA", consumerSecret="WX9dUXrTQsoESifTtzM4mQgtfJTCq7JPMApm8FrxisY",
                               requestURL="https://api.twitter.com/oauth/request_token" ,
                               accessURL="https://api.twitter.com/oauth/access_token",
                               authURL="https://api.twitter.com/oauth/authorize")
#view credentials
credential

#get AuthURL pin (note: can't copy and paste oauth_token and it's VERY long so be careful typing, you only get one chance)
credential$handshake(cainfo = system.file("CurlSSL", "cacert.pem", package = "RCurl"))
registerTwitterOAuth(credential)
#save credentials, use the load function later
save(credential, file="credentials.RData")

SearchTweets <- function(){#Search function
  tweetList1<- searchTwitter("Ford", n=250)
  tweetList2<- searchTwitter("General Motor", n=25)

  
  # str(head(tweetList,1))
  
  #Merge the tweetlist into one object so that it's easier to put them into one dataframe
  #joinTweets<- c(tweetList1,tweetList2, tweetList3, tweetList4, tweetList5,tweetList6, tweetList7,tweetList8, tweetList9, tweetList10, tweetList11 )
  joinTweets<- c(tweetList1,tweetList2)
  # put data into a dataframe
  tweetDF <- do.call("rbind", lapply(joinTweets,as.data.frame))
  
  #Cumulative dataframe
  CTweets<- c()
  CTweets<- rbind(CTweets, tweetDF)
  
  #Remove dublicate Tweets
  CTweets <-unique(CTweets)
  
  #Backup CTweets by writing to an external csv file
  write.csv(CTweets, file="tweets_9_22.csv",row.names=F)
  
  return(CTweets)
}

tweetdata <- SearchTweets()
print(nrow(tweetdata))
tweetdata[,]
doc<-sample(225,size=100)
doc

wantedsample <- tweetdata[doc, ]

head(wantedsample)
write.csv(tweetdata, file="wantedsample.csv",row.names=F)

# Create a copy of your cumulative tweets dataframe.  *

A4<-tweetdata

frequency(A4$screenName)

frequency(A4$screenName=="evinante")

#  b. Categorize the variables retweeted and favorited
A4$favorited<-as.factor(A4$favorited)
A4$retweeted<-as.factor(A4$retweeted)

#  c. New variable for whether each tweet has been retweeted by any other Twitter users.
user.retweet<-rep(NA,225)
A4$user.retweet<-A4$retweetCount>=1


#  d.New variable for whether each tweet has been favorited by any other Twitter users.
user.fav<-rep(NA,225)
A4$user.fav<-A4$favoriteCount>=1


#  e.New variable indicating whether each tweet has been either favorited or retweeted (vs. neither favorited nor

#   retweeted).

fav.retw<-rep(NA,225)
A4$fav.retw<- A4$user.retweet | A4$user.fav


# 3. Run frequency tables (using freq() ) of all the variables

#  from each part of this assignment, and copy & paste into

#  a Word doc or text file to upload for this assignment (in

#  addition to this .R file containing your commands)

table(A4$fav.retw, A4$user.retweet, A4$user.fav)
table (A4$fav.retw)
table(A4$user.retweet)
table(A4$user.fav)

#Backup CTweets by writing to an external csv file
write.table(A4, file="tweets_9_22.txt", sep="\t",row.names=F)

hist(A4$created, breaks=15, frequency=T)
sortedTweets<- A4[order(as.integer(A4$created)),]
inter.Tweet.interval<-diff(sortedTweets$created)
hist(as.integer(inter.Tweet.interval), breaks=15, xlim=range(0,60000))
mean(inter.Tweet.interval)
median(inter.Tweet.interval)
as.numeric(names(which.max(table(inter.Tweet.interval))))
poisson.rand<-rpois(200,2884)
hist(poisson.rand,xlim=range(0,2885))
mean(poisson.rand)
var(poisson.rand)

sum((as.integer(diff(inter.Tweet.interval)))<60)
sum((as.integer(diff(inter.Tweet.interval)))<60)/length(inter.Tweet.interval)