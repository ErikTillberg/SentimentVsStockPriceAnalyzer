#Support Vector Machine to analyze stock price & twitter sentiment

#install.packages("e1071")
library("e1071")
library(jsonlite)

set.seed(1)

load("twitterStockData_TSLA.rda")

compound = json_data$sentiment$compound
positive = json_data$sentiment$positive
negative = json_data$sentiment$negative

stockChange = json_data$stockChange

dat = data.frame(c = compound, p=positive,n=negative, s = stockChange)

train = sample(1:nrow(dat),nrow(dat)*0.75)
test = -train

training_data = total_data[train,]
test_data = total_data[test,]

testing_result = dat$stockChange[test]

svmfit = svm(testing_result, data = dat[train,], kernel = "linear", cost = 10, scale = FALSE)
summary(svmfit)

#predictions:
predictions = predict(svmfit, test_data)
predictions
