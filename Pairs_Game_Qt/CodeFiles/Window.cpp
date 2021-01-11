#include <QApplication>
#include <QMainWindow>
#include <QLabel>
#include <QPushButton>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QSpacerItem>
#include <QGridLayout>
#include "clock.h"
#include "score.h"
#include "result.h"
#include "wordcard.h"
#include <vector>
#include <table.h>
#include "active.h"
#include <QTimer>


int main(int argc, char *argv[])
{
    QApplication game(argc,argv);               // General application
    QMainWindow * window = new QMainWindow();   // Main window of game
    Clock *clock = new Clock(180);              // Timer initialization
    Score *score = new Score();                 // ScoreBoard initialization
    Result *result = new Result(score);         // Result dialogs initialization
    QWidget *board = new QWidget();             // Dumb widget that keeps layouts
    Active * active = new Active(clock->clock); // Active cards checker initialization

    // List of words that will be used
    std::vector<QString> list{"Mostly","Harmles","Hazar","Cakir","Emir","Arthur","Dent", "Earth","So","Long","Thanks","For","All","The","Fish","Mostly","Harmles","Hazar","Cakir","Emir","Arthur","Dent", "Earth","So","Long","Thanks","For","All","The","Fish"};


    QPushButton *newGame = new QPushButton  ("New Game");   // New game button
    QPushButton *quit = new QPushButton("Quit");            // Quit button


    QVBoxLayout *v1 = new QVBoxLayout();                    // First vertical layout
    QHBoxLayout *h1 = new QHBoxLayout();                    // First horizontal layout which will be in vertical layout
    Table *table = new Table(active,&list);                 // Game board initialization
    QSpacerItem *sp = new QSpacerItem(10,0,QSizePolicy::Expanding, QSizePolicy::Minimum); // Spacer item between score and new game button

    h1->addWidget(clock->display);  // Timer display
    h1->addWidget(score->display);  // Score display
    h1->addSpacerItem(sp);          // Spacer
    h1->addWidget(newGame);         // New game button
    h1->addWidget(quit);            // quit button


    table->create();                // This creates cards in random order and put them in a grid layout.
    v1->addLayout(h1);              // First horizontal layout
    v1->addLayout(table);           // Table is under the first horizontal layout
    v1->addSpacerItem(new QSpacerItem(0,10,QSizePolicy::Minimum, QSizePolicy::Expanding));      // This pushes all items up
    v1->setSpacing(10);
    v1->spacing();


    // Main window arrangaments
    board->setLayout(v1);
    window->setCentralWidget(board);
    window->setWindowTitle("Word Game");
    window->resize(640,300);
    window->show();

    // Signals and connections
    QObject::connect(quit,SIGNAL(clicked()), &game, SLOT(quit()));
    QObject::connect(clock,SIGNAL(endgame()) , result, SLOT( evaluate() ) );
    QObject::connect(score,SIGNAL(endgame()) , result, SLOT( evaluate() ) );
    QObject::connect(result, SIGNAL(quit()), &game, SLOT(quit()));
    QObject::connect(result, SIGNAL(freeze()), clock, SLOT(stop()));
    QObject::connect(result, SIGNAL(newGame()), newGame, SIGNAL(clicked()));
    QObject::connect(active, SIGNAL(disableAll()), table, SLOT(disable()));
    QObject::connect(active, SIGNAL(enableAll()), table, SLOT(enable()));
    QObject::connect(active, SIGNAL(score()), score, SLOT(scoreUp()));
    QObject::connect(newGame, SIGNAL(clicked()), active, SLOT(restart()));
    QObject::connect(newGame, SIGNAL(clicked()), clock, SLOT(restart()));
    QObject::connect(newGame, SIGNAL(clicked()), score, SLOT(restart()));
    QObject::connect(newGame, SIGNAL(clicked()), table, SLOT(restart()));








    return game.exec();
}
