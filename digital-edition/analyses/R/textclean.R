#This function takes a single text and returns the text
#without punctuation or numbers
text.clean<-function(text){
  #first, convert text to lower
  text.lower<-tolower(text)
  #then, split the text into characters
  text.letters<-unlist(strsplit(text.lower, ""))
  #then find which characters aren't letters
  bad.index<-which(!text.letters %in% letters)
  #then, find which characters are hyphens
  hyphen.index<-which(text.letters=="-")
  #then, convert hyphens into spaces
  text.letters[hyphen.index]<-" "
  #then, find the location of the spaces
  space.index<-which(text.letters==" ")
  #find which things in bad.index are spaces
  spaces.in.bad<-which(bad.index %in% space.index)
  #remove the spaces from bad.index
  bad.index<-bad.index[-spaces.in.bad]
  #remove all of the non letters from the character vector
  text.letters<-text.letters[-bad.index]
  #collapse the character vector back into the text
  text.final<-paste(text.letters, collapse="")
  #finally, return the cleaned text
  return(text.final)
}

#function to grab chunks of text around a target word, size of
#chunk is equal to horizon
kwic<-function(target.keyword, text.words, horizon){
  #find the places in text.words where the target.keyword can be 
  #found
  target.index<-which(text.words==target.keyword)
  #create an empy variable to be filled with the results of each
  #kwic
  target.kwics<-NULL
  #a loop that repeats as many times as there are incidents of our
  #target keyword in our text words
  for (i in 1:length(target.index)){
    #if our first target.keyword minus our horizon is less than
    #1 (the beginning of the text) then...
    if (target.index[i]-horizon<1){
      #set our start variable to 1 (the beginning of text)
      start<-1
    #if our first target.keyword minus our horizon is not less
    #than 1 then...
    } else {
      #set start equal to target.keyword location minus horizon
      start<-target.index[i]-horizon
    }
    #if target.keyword location plus horizon is more than the number
    #of words in the text then..
    if (target.index[i]+horizon>length(text.words)){
      #set end variable to the end of the text
      end<-length(text.words)
    #if target.keyword location plus horizon is not more than the number
    #of words in the text, then...
    } else {
      #set end to target.index plus our horizon
      end<-target.index[i]+horizon
    }
    #with the start and end variables we created, grab a chunk of text
    #from text.words, from start to end
    text.chunk<-text.words[start:end]
    #collapse the chunk of text from individual words to a single
    #variable separated by spaces
    text.chunk<-paste(text.chunk, collapse=" ")
    #add our new text.chunk to our running list of text chunks
    target.kwics<-c(target.kwics, text.chunk)
  }
  #return our complete list of text chunks
  return(target.kwics)
}

getCorpus<-function(dir, type=".txt"){
  #finds the current folder and saves it
  curr.folder<-getwd()
  #change folder to the one with texts
  setwd(dir)
  #get list of files
  file.list<-list.files(pattern=type)
  #create an empty place called corpus to put the texts
  corpus<-NULL
  #for each filename in our list
  for (i in 1:length(file.list)){
    #scan file from current filename in file.list, separate by newlines
    curr.text<-scan(file.list[i], what="character", sep="\n")
    #paste file back together using the same character
    curr.text<-paste(curr.text, collapse="\n")
    #add the new text to our corpus
    corpus<-c(corpus, curr.text)
  }
  #name elements of new corpus with filenames
  names(corpus)<-file.list
  #set working directory back to original folder
  setwd(curr.folder)
  #return our corpus
  return(corpus)
}

#take corpus and clean texts in it
clean.corpus<-function(corpus){
  #for 1 to the length of the corpus..
  for (i in 1:length(corpus)){
    cleaned.text<-text.clean(corpus[i])
    corpus[i]<-cleaned.text
  }
  return(corpus)
}

#count unique words in each text and combine into a single table
createDTM<-function(corpus){
  #create an empty list for individual text wordcounts
  word.counts<-list()
  #for loop to count words in each text and put result in list
  for (i in 1:length(corpus)){
    #take the first text and split it by spaces
    text.words<-unlist(strsplit(corpus[i], " "))
    #create a table of word frequencies for that text
    curr.freqs<-table(text.words)
    #find empty names in table of word frequencies
    bad.index<-which(names(curr.freqs)=='')
    #delete empty names
    curr.freqs<-curr.freqs[-bad.index]
    #add current table of frequencies to list
    word.counts<-c(word.counts, list(curr.freqs))
  }
  #make the names of the list, the same as the names of the corpus
  names(word.counts)<-names(corpus)
  #create an empty data frame to put our word counts into
  dtm<-data.frame()
  #for each text in our list of text word frequencies
  for(i in seq(along=word.counts)){
    #for the frequency of each word in that text
    for(j in names(word.counts[[i]])){
      #the cell of the dataframe that we created equal to the text and
      #letter adds the value of that frequency from our list or
      #if not already there, creates a new column for that word
      dtm[i,j]<-word.counts[[i]][[j]]
    }
  }
  #add rownames to dtm
  rownames(dtm)<-names(corpus)
  for(i in 1:nrow(dtm)){
    curr.row<-dtm[i,]
    na.index<-which(is.na(curr.row))
    curr.row[na.index]<-0
    dtm[i,]<-curr.row
  }
  #return the data frame as a dtm
  return(dtm)
}

#function to grab chunks of text around a target word, size of
#chunk is equal to horizon
multi.kwic<-function(keyword.list, distance.between, text.words, horizon){
  keyword1.index<-which(text.words == keyword.list[1])
  keyword2.index<-which(text.words == keyword.list[2])
  keyword.pairs<-list()
  
  for (i in 1:length(keyword1.index)){
    key1<-keyword1.index[i]
    for (j in 1:length(keyword2.index)){
      distance.k1k2<-abs(key1-keyword2.index[j])
      if (distance.k1k2 <= distance.between){
        match.pair<-c(key1, keyword2.index[j])
        match.pair<-sort(match.pair) #sort to make sure word index is in order to prevent using horizon check in the wrong direction
        keyword.pairs<-c(keyword.pairs,list(match.pair))
      }
    }
  }
  print(length(keyword.pairs)) #print to debug
  if (length(keyword.pairs)==0){
    print("No character pair found.")
  } else {
    #create an empy variable to be filled with the results of each
    #kwic
    target.kwics<-NULL
    #a loop that repeats as many times as there are incidents of our
    #target keyword in our text words
    for (i in 1:length(keyword.pairs)){
      curr.pair<-keyword.pairs[[i]]
      #if our first target.keyword minus our horizon is less than
      #1 (the beginning of the text) then...
      if (curr.pair[1]-horizon<1){
        #set our start variable to 1 (the beginning of text)
        start<-1
        #if our first target.keyword minus our horizon is not less
        #than 1 then...
      } else {
        #set start equal to target.keyword location minus horizon
        start<-curr.pair[1]-horizon
      }
      #if target.keyword location plus horizon is more than the number
      #of words in the text then..
      if (curr.pair[2]+horizon>length(text.words)){
        #set end variable to the end of the text
        end<-length(text.words)
        #if target.keyword location plus horizon is not more than the number
        #of words in the text, then...
      } else {
        #set end to target.index plus our horizon
        end<-curr.pair[2]+horizon
      }
      #with the start and end variables we created, grab a chunk of text
      #from text.words, from start to end
      text.chunk<-text.words[start:end]
      #collapse the chunk of text from individual words to a single
      #variable separated by spaces
      text.chunk<-paste(text.chunk, collapse=" ")
      #add our new text.chunk to our running list of text chunks
      target.kwics<-c(target.kwics, text.chunk)
    }
    #return our complete list of text chunks
    return(target.kwics)
  }
}