library(shiny)
library(ggplot2)
library(gridExtra)
library(rjson)
library(ggthemes)
library(dplyr)
require("jsonlite")
require("httr")

#Import datas from lille
data=read.csv("https://opendata.lillemetropole.fr/explore/dataset/indice-qualite-de-lair/download/?format=csv&timezone=Europe/Berlin&use_labels_for_header=true", head=TRUE, sep=";")
keeps = c("date_ech", "valeur")
data = data[keeps]
names(data)[names(data)=="date_ech"] <- "date"
data$date <- as.Date(data$date, "%Y-%m-%d")

#Import datas from our API
url = "https://airiq-271312.appspot.com//"
command = "allpredictions"
request = paste(url, command, sep="")
prediction <- GET(request)
prediction <- fromJSON(content(prediction, "text"))
prediction <- lapply(prediction, function(x) {
  x[sapply(x, is.null)] <- NA
  unlist(x)
})
df_prediction<-as.data.frame(do.call("cbind", prediction))
df_prediction$value = as.numeric(as.character(df_prediction$value))
df_prediction$dateofprediction = as.Date(df_prediction$dateofprediction, format = "%Y-%m-%d")
names(df_prediction)[names(df_prediction)=="dateofprediction"] <- "date"
names(df_prediction)[names(df_prediction)=="value"] <- "predictValue"

# mix both data:
concat_df = left_join(df_prediction, data, by="date")
listOfdf = split(concat_df, concat_df$typeofprediction)

ui <- navbarPage("AirIQ - Vizualize our results",
                 # First page
                 tabPanel("Prediction",
                          sidebarLayout(
                            sidebarPanel(
                              selectInput("IQ",
                                          label = "Choose a prediction to display", 
                                          choices = c("Prediction J+1","Prediction J+2","Prediction J+3"),
                                          selected = "Prediction J+1")
                              
                            ),
                            # Show
                            mainPanel(
                              plotOutput("PredictionGraph")
                            )
                          )
                 ),
                 # Second page
                 tabPanel("Air index quality",
                          sidebarLayout(
                            sidebarPanel("Data collected from the MEL API :",
                                         dateRangeInput('dateRangeIQ',
                                                        label = 'Date range input: yyyy-mm-dd',
                                                        start = as.Date("2019-01-01"), end = Sys.Date())
                            ),
                            
                            # Show
                            mainPanel(
                              plotOutput("dateRangeIQ")
                            )
                          )
                 )
)

# Define server logic required to draw a histogram
server <- function(input, output) {
  output$PredictionGraph <- renderPlot({
    # Retrieve data
    number <- switch(input$IQ, 
                   "Prediction J+1" = 1,
                   "Prediction J+2" = 2,
                   "Prediction J+3" = 3)
    
    #graph
    p = ggplot(data=listOfdf[[number]], aes(x=date)) +
      
      ylim(0,10)+
      
      geom_line(aes(y=predictValue), 
                color = "darkred", 
                linetype="twodash") +
      geom_point(aes(y=predictValue),
                 shape=21, color="black", 
                 fill="darkred", 
                 size=4)+
      
      geom_line(aes(y = valeur), 
                color=rgb(0.1,0.7,0.1,0.8))  +
      geom_point(aes(y=valeur),
                 shape=21, color="black", 
                 fill=rgb(0.1,0.7,0.1,0.8), 
                 size=4)+
      ggtitle(sprintf("Prediction J+%s",number))+
      
      theme_hc()
    grid.arrange(p,ncol=1)
  })
  
  output$dateRangeIQ <- renderPlot({
    p1=ggplot(data = data, aes(x = date, y = valeur))+
      geom_line(color = rgb(0.1,0.7,0.1,0.8), size = 0.5)+ xlim(input$dateRangeIQ)+
      theme_hc()
    
    date = data[data$date >= input$dateRangeIQ[1] & data$date <= input$dateRangeIQ[2],]
    
    p2=qplot(date$valeur,
             geom="histogram",
             breaks=seq(0, 10, by = 1),
             binwidth = 1,
             fill=I(rgb(0.1,0.7,0.1,0.8)), 
             col=I("black"),
             main = "Histogram of IQ values", 
             xlab = "Index",
             xlim=c(1,10))+
      theme_hc()
    
    grid.arrange(p1,p2, ncol=1)
  })
}

# Run the application 
shinyApp(ui = ui, server = server)