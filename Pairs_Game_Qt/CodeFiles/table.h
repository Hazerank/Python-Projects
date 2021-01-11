#ifndef TABLE_H
#define TABLE_H

#include <QObject>
#include <QGridLayout>
#include "wordcard.h"
#include "active.h"

class Table : public QGridLayout
{
    Q_OBJECT


public:
    Table(Active *active,std::vector<QString> * list);
    Active *active;                 // Pointer of "Active" class. This is needed because a signal-slot binding happens inside of the methods.
    std::vector<QString> *list;     // List of words that will be behind the cards
    void create();                  // Creates all cards and table with list field randomly.


public slots:
    void disable();             // Sets disabled all cards in the grid
    void enable();              // Sets enabled all cards in the grid
    void restart();             // Handles restart situation. Resets corresponding fields.

};

#endif // TABLE_H
