#Web Scraping HTML:

install.packages("rvest")
install.packages("dplyr")

library(dplyr)
library(rvest)

"------------------------------------------------------------------------------"
"------------------------------------------------------------------------------"

#USFA DIV 1 OCT NAC 2012

url <- "https://www.usfencingresults.org/results/2012-2013/2012-10-OCT%20NAC/FTEvent_2012Oct12_DV1ME.htm"
webpage <- read_html(url)

pools_html <- html_nodes(webpage, ".poolScoreCol")
pools <- html_text(pools_html)
(pools)

names_html <- html_nodes(webpage, ".poolNameCol")
names <- html_text(names_html)
(names)

data <- cbind(pools, names)
Number <- 1:7

data <- data.frame(input = character(length(names)))
data$names <- names
data$Number <- rep(Number, len=(length(names)))

pools[1]
pools[9]
#change the pools into pool format by traversing through the pool results
#and everytime "" appears it should append a row 

data_creator <- function() {
  
  for (i in range(length(pools))) {
    data <- data.frame

  
    if ((pools[i] == "") & (pools[i+9] == "")) {
      row = NULL
      count <- 7
      for (j in range(length(count))) {
        row <- append(row, pools[i+j])
    }
      rbind(data, row)
    }
    else {
      row = NULL
      count <- 6
      for (k in rnage(length(count))) {
        row <- append(row, pools[i+k])
    }
      rbind(data, row)
  }
  }
}

