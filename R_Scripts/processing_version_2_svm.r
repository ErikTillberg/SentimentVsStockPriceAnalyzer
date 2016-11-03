#Support Vector Machine to analyze stock price & twitter sentiment

#install.packages("e1071")
library(tree)
library(rpart)
library("e1071")

set.seed(1)

load("twitterStockData_TSLA.rda")
stock_dat = read.csv("AAPL.csv", header=TRUE)

plot((stock_dat$DATE-stock_dat$DATE[1])/(3600*24), stock_dat$CLOSE)
plot((json_data$timestamp_sec-json_data$timestamp_sec[1])/(3600*24), json_data$stock_changes$`24`)

total_data = data.frame(
  sentiment_pos = json_data$sentiment$pos,
  sentiment_neg = json_data$sentiment$neg,
  sentiment_neu = json_data$sentiment$neu,
  sentiment_cmp = json_data$sentiment$compound,
  #stock_change = json_data$stock_changes$`24`
  stock_change = ifelse(json_data$stock_changes$`24`>=0, "Yes", "No")
)

train = sample(1:nrow(total_data),nrow(total_data)*0.75)
test = -train

training_data = total_data[train,]
test_data = total_data[test,]

svmfit = svm(stock_change~., data = training_data, kernel = "linear", cost = 10, scale = FALSE)
summary(svmfit)

predictions = predict(svmfit, test_data)
predictions

table(predictions, test_data$stock_change)
