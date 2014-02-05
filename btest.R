btest <- function() {
  
sess <- read.csv( "data/sessions.dat", header = TRUE, sep = " ", colClasses = "character")
talk <- read.csv( "data/talks.dat", header = TRUE, sep = " ", colClasses = "character" )
data <- read.csv( "data/questions.dat", header = TRUE, sep = " " )

talk$speaker <- as.character(talk$speaker)
talk$id <- as.character(talk$id)

talkid <- as.numeric(str_sub(talk$id,-2))
talkmain <- as.numeric(substring(talk$id,1,3))
speak <- talk$speaker
dataframe <- data.frame(talkmain,talkid,speak)

results <- rep(0, 151)
talks <- rep(0, 151)

n <- 1
  
for (i in 1:(NROW(talkmain)-1)) {
  mainid <- talkmain[i]
  if (mainid != talkmain[i+1]) {
    dataframe_sub<-dataframe[dataframe$talkmain==mainid, ]  
    talks[n] <- mainid
    numtalks <- max(dataframe_sub$talkid)
    numtalksM <- as.numeric(NROW(dataframe_sub[dataframe_sub$speak=='m',]))
    numtalksF <- as.numeric(NROW(dataframe_sub[dataframe_sub$speak=='f',]))    
    if (numtalksF < 2) { results[n] <- 0                        
    }else {results[n] <- 1 }  
    n<-n+1
  }
}
totresults <- data.frame(talks,results)  
totalpass <- sum(results)
return(totresults)
}
