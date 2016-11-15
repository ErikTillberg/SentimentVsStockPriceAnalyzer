setwd("C:/Users/Steven/Documents/Programming/Git Repositories/Remote Repositories/SentimentVsStockPriceAnalyzer/R_Scripts")
library(jsonlite)

data_name <- "tesla filtered_filtered_no_garbage_filtered.json"

json_data <- fromJSON(txt=data_name)

names(json_data)
head(json_data, n=3)

save(json_data, file=paste(data_name, "rda", sep="."))
