#Support Vector Machine to analyze stock price & twitter sentiment

#install.packages("e1071")
library(tree)
library(rpart)
library("e1071")

set.seed(1)

load("tesla filtered_filtered_no_garbage_filtered.json.rda")
#stock_dat = read.csv("AAPL.csv", header=TRUE)

plot((stock_dat$DATE-stock_dat$DATE[1])/(3600*24), stock_dat$CLOSE)
plot((json_data$timestamp_sec-json_data$timestamp_sec[1])/(3600*24), json_data$stock_changes$`24`)

total_data = data.frame(
  sentiment_pos = json_data$sentiment$pos,
  sentiment_neg = json_data$sentiment$neg,
  sentiment_neu = json_data$sentiment$neu,
  sentiment_cmp = json_data$sentiment$compound,
  #stock_change = json_data$stock_changes$`24`
  stock_change = ifelse(json_data$stock_changes$`48`>=0, "Yes", "No")
)
hist(total_data$sentiment_cmp, xlab= "Body Mass Index", main="Distribution of tweet sentiment: Tesla")
train = sample(1:nrow(total_data),nrow(total_data)*0.75)
test = -train

training_data = total_data[train,]
test_data = total_data[test,]
#na.omit(training_data)
#tune.out=tune(svm, stock_change~., data=training_data, kernel = "radial", 
#              ranges = list(cost=c(0.1,1,10),
#                            gamma=c(0.5,2,4)))

summary(tune.out)
predictions = predict(tune.out$best.model, news=test_data)
table(predictions, test_data$stock_change)

svmfit = svm(training_data$stock_change~., data = training_data, kernel = "radial", gamma = 0.25, cost = 10000, scale = FALSE)
summary(svmfit)

predictions = predict(svmfit, test_data)

t <- table(predictions, test_data$stock_change)
success <- ((t[1]+t[4])/(t[1]+t[2]+t[3]+t[4]))
success
