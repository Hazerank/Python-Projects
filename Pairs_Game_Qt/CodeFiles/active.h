#ifndef ACTIVE_H
#define ACTIVE_H

#include <QObject>
#include "wordcard.h"
#include <vector>
#include <QTimer>


class Active : public QObject
{

    Q_OBJECT


public:
    Active(QTimer *main);
    std::vector<WordCard*> * activeList;    // List of active cards. It can include max 2 item.
    QTimer * cooldown;                 // The timer to implement the waiting time of wrong try.
    QTimer * main;                     // The field of main timer of game. It is included in order to halt it but the stopping option removed later.
    WordCard *w1;                      // The first WordCard in the list
    WordCard *w2;                      // The second WordCard in the list

signals:
    void enableAll();               // Emitted when controll process done and its enables all other closed cards
    void disableAll();              // Emitted when controll process is in process and disables all other closed cards.
    void score();                   // If there is a succesfull coupling, this signal emitted and it is catched by "Score" class

public slots:
    void process(WordCard *one);    // It process active card corresponding to the situation.
    void free();                    // It frees the waiting situation in the wrong coupling
    void restart();                 // It resets corresponding fields
};

#endif // ACTIVE_H
