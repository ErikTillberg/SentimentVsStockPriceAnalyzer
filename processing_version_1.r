setwd("C:/Users/Steven/Documents/Programming/Git Repositories/Remote Repositories/SentimentVsStockPriceAnalyzer")
library(jsonlite)
library(tree)

load("tsla.rda")
stock_dat = read.csv("TSLA.csv", header=TRUE)

names(json_data)
names(stock_dat)

#head(stock_dat)

#stock_dat$CLOSE[-(1:10)]

time_diff <- 7#*60
x <- stock_dat$CLOSE[-(1:time_diff)]-stock_dat$CLOSE[(1:(length(stock_dat$CLOSE)-time_diff))]
y <- stock_dat$DATE[(1:(length(stock_dat$DATE)-time_diff))]
plot(x)
plot(stock_dat$CLOSE)

sentiment = rep(0, length(json_data$sentiment$result$confidence))
sentiment[json_data$sentiment$result$sentiment=="Positive"] = 1
sentiment[json_data$sentiment$result$sentiment=="Negative"] = -1
sentiment = sentiment*json_data$sentiment$result$confidence

stock_dat_proc = data.frame(
  change=x,
  time=y
)

twitter_data_proc = data.frame(
  sentiment=sentiment,
  time=json_data$timestamp_sec
)

temp <- rep(NaN, length(twitter_data_proc$time))
for (i in 1:length(temp)){
  temp[i] = which.min(abs(stock_dat_proc$time - twitter_data_proc$time[i]))
}
#plot(temp)

sum_ <- rep(0, length(stock_dat_proc$time))
count_ <- rep(0, length(stock_dat_proc$time))
for (i in 1:length(temp)){
  t = temp[i]
  #if (twitter_data_proc$sentiment[i] != 0){
  sum_[t] = sum_[t]+twitter_data_proc$sentiment[i]
  count_[t] = count_[t]+1
  #}
}

avg_ = sum_/count_
#avg_[count_< 20] = NaN

test = rep(0, length(avg_))
for (i in 1:length(test)){
  test[i] = nchar(json_data$text[i])
}


#start<-150
start<-0
end<-length(avg_)
#end<-length(avg_)*0.75
total_data = data.frame(
  sentiment=avg_[(start:end)],
  #time=stock_dat_proc$time[(start:length(stock_dat_proc$change))],
  #change=stock_dat_proc$change[(start:length(stock_dat_proc$change))]>0
  change=ifelse(stock_dat_proc$change[(start:end)]>=0, "Yes", "No")
  #str_len=test
)

total_data_2 = data.frame(
  sentiment=avg_[(start:end)],
  #time=stock_dat_proc$time[(start:length(stock_dat_proc$change))],
  #change=stock_dat_proc$change[(start:length(stock_dat_proc$change))]>0
  change=stock_dat_proc$change[(start:end)]
  #str_len=test
)

set.seed(2)

train = sample(1:nrow(total_data),nrow(total_data)*0.75)
test = -train
training_data = total_data[train,]
test_data = total_data[test,]
testing_result = total_data$change[test]

tree_model = tree(change~., training_data)
plot(tree_model)
text(tree_model, pretty=0)

tree_predict=predict(tree_model, test_data, type = "class")
mean(tree_predict!=testing_result)

pruned_model=prune.misclass(tree_model, best = 2)
plot(pruned_model)
text(pruned_model, pretty=0)

tree_pred=predict(pruned_model, test_data, type="class")
mean(tree_pred!=testing_result)

fit <- lm(change ~ sentiment, data=total_data_2)
summary(fit) # show results
#plot(sentiment ~ change, data=total_data_2)
#plot(change ~ sentiment, data=total_data_2)
plot(total_data_2$sentiment, total_data_2$change)
coef(fit)
abline(lm(change ~ sentiment, data=total_data_2), col="red")
#plot(fit)



fit = glm(change ~ sentiment, data=total_data_2)
summary(fit) # show results
plot(change ~ sentiment, data=total_data_2)
abline(fit, col="red")

curve(predict(fit,data.frame(sentiment=x),type="resp"),add=TRUE)
