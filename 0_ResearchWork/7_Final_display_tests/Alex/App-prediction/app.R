library(shiny)
library(ggplot2)
library(gridExtra)
library(rjson)

#Import datas from lille
data=read.csv("https://opendata.lillemetropole.fr/explore/dataset/indice-qualite-de-lair/download/?format=csv&timezone=Europe/Berlin&use_labels_for_header=true", head=TRUE, sep=";")
keeps = c("date_ech", "valeur")
data = data[keeps]
data$date_ech <- as.Date(data$date_ech, "%Y-%m-%d")

ui <- navbarPage("AirIQ - Vizualize our results",
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
  
  output$dateRangeIQ <- renderPlot({
    p1=ggplot(data = data, aes(x = date_ech, y = valeur))+
      geom_line(color = "orange", size = 0.5)+ xlim(input$dateRangeIQ)
    
    date = data[data$date_ech >= input$dateRangeIQ[1] & data$date_ech <= input$dateRangeIQ[2],]
    
    p2=qplot(date$valeur,
             geom="histogram",
             breaks=seq(0, 10, by = 1),
             binwidth = 1,
             fill=I("orange"), 
             col=I("red"),
             main = "Histogram of IQ values", 
             xlab = "Index",
             xlim=c(1,10))
    
    grid.arrange(p1,p2, ncol=1)
  })
}

# Run the application 
shinyApp(ui = ui, server = server)