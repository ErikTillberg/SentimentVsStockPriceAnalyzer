setwd("C:/Users/Steven/Documents/Programming/Git Repositories/Remote Repositories/SentimentVsStockPriceAnalyzer")
library(jsonlite)

data_name <- "tsla"

json_file <- paste(data_name, "fixed.json", sep=".")
json_data <- fromJSON(txt=json_file)

names(json_data)
head(json_data, n=3)

save(json_data, file=paste(data_name, "rda", sep="."))
