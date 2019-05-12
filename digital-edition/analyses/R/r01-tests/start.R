# load character vectors 
eb03.v <- scan ('eb03/eb03-all.txt', what="character", sep='\n')
eb07.v <- scan ('eb07/eb07-all.txt', encoding = "UTF-8", what="character", sep='\n')
eb09.v <- scan ('eb09/eb09-all.txt', encoding = "UTF-8", what="character", sep='\n')
eb11.v <- scan ('eb11/eb11-all.txt', encoding = "UTF-8", what="character", sep='\n')

#test character vectors
eb03.v[1:10]
eb07.v[1:10]
eb09.v[1:10]
eb11.v[1:10]

#reprocess the content
eb03.lc.v <- tolower(eb03.v)
eb07.lc.v <- tolower(eb07.v)
eb09.lc.v <- tolower(eb09.v)
eb11.lc.v <- tolower(eb11.v)

eb03.word.l <- strsplit(eb03.lc.v, "\\W")
eb07.word.l <- strsplit(eb07.lc.v, "\\W")
eb09.word.l <- strsplit(eb09.lc.v, "\\W")
eb11.word.l <- strsplit(eb11.lc.v, "\\W")

eb03.word.v <- unlist(eb03.word.l) 
eb07.word.v <- unlist(eb07.word.l) 
eb09.word.v <- unlist(eb09.word.l) 
eb11.word.v <- unlist(eb11.word.l) 

eb03.notblank.v <- which(eb03.word.v!="")
eb07.notblank.v <- which(eb07.word.v!="")
eb09.notblank.v <- which(eb09.word.v!="")
eb11.notblank.v <- which(eb11.word.v!="")

eb03.word.v <- eb03.word.v[eb03.notblank.v]
eb07.word.v <- eb07.word.v[eb07.notblank.v]
eb09.word.v <- eb09.word.v[eb09.notblank.v]
eb11.word.v <- eb11.word.v[eb11.notblank.v]

#BEGIN ANALYSIS

#calculate ttr
eb03.total.words.v <- length(eb03.word.v)
eb03.unique.words.v <- length (unique(eb03.word.v))
eb03.unique.words.v
eb03.total.words.v
eb03.unique.words.v/eb03.total.words.v

eb07.total.words.v <- length(eb07.word.v)
eb07.unique.words.v <- length (unique(eb07.word.v))
eb07.unique.words.v
eb07.total.words.v
eb07.unique.words.v/eb07.total.words.v

eb09.total.words.v <- length(eb09.word.v)
eb09.unique.words.v <- length (unique(eb09.word.v))
eb09.unique.words.v
eb09.total.words.v
eb09.unique.words.v/eb09.total.words.v

eb11.total.words.v <- length(eb11.word.v)
eb11.unique.words.v <- length (unique(eb11.word.v))
eb11.unique.words.v
eb11.total.words.v
eb11.unique.words.v/eb11.total.words.v

eb03c.total.words.v <- length(eb03-all.word.v)
eb03.unique.words.v <- length (unique(eb03.word.v))
eb03.unique.words.v
eb03.total.words.v
eb03.unique.words.v/eb03.total.words.v


#create and output word frequency tables as .csv files
eb03.freqs.t <- table(eb03.word.v)
sorted.eb03.freqs.t <- sort (eb03.freqs.t, decreasing = TRUE)
sorted.eb03.freqs.t[1:50]
write.csv(sorted.eb03.freqs.t, 'eb03.csv')

eb07.freqs.t <- table(eb07.word.v)
sorted.eb07.freqs.t <- sort (eb07.freqs.t, decreasing = TRUE)
sorted.eb07.freqs.t[1:50]
write.csv(sorted.eb07.freqs.t, 'eb07.csv')

eb09.freqs.t <- table(eb09.word.v)
sorted.eb09.freqs.t <- sort (eb09.freqs.t, decreasing = TRUE)
sorted.eb09.freqs.t[1:50]
write.csv(sorted.eb09.freqs.t, 'eb09.csv')

eb11.freqs.t <- table(eb11.word.v)
sorted.eb11.freqs.t <- sort (eb11.freqs.t, decreasing = TRUE)
sorted.eb11.freqs.t[1:50]
write.csv(sorted.eb11.freqs.t, 'eb11.csv')

#plot word frequencies
top.words.v <- c(sorted.eb03.freqs.t[1:10])
plot(top.words.v)

top.words.v <- c(sorted.eb07.freqs.t[1:10])
plot(top.words.v)

top.words.v <- c(sorted.eb09.freqs.t[1:10])
plot(top.words.v)

top.words.v <- c(sorted.eb11.freqs.t[1:10])
plot(top.words.v)


