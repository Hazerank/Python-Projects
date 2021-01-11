#include "table.h"

/**
 * I make use of Ps codes in this class a bit.
 *
 * @brief Table::Table initializes fields with default values
 * @param active
 * @param list
 */
Table::Table(Active *active,std::vector<QString> *list):QGridLayout()
{
    this->active = active;
    this->list = list;
}
/**
 * Sets enabled all cards in the grid by changing act fields as true;
 *
 *
 * @brief Table::enable
 */
void Table::enable(){
    for(int i = 0 ; i < this->count() ; i++){
        qobject_cast<WordCard*>(this->itemAt(i)->widget())->act = true;
    }
}

/**
 *  Sets disabled all cards in the grid by changing act fields as false;
 *
 *
 * @brief Table::disable
 */
void Table::disable(){
    for(int i = 0 ; i < this->count() ; i++){
        qobject_cast<WordCard*>(this->itemAt(i)->widget())->act = false;
    }
}
/**
 * Suffles list field and creates all cards and grid regarding to shuffled list.
 * As manuel, table size is determined as 6x4, and implemented as this way.
 *
 * It connects every WordCards active signal to active's process slot
 *
 * @brief Table::create
 */
void Table::create(){
    std::srand(time(0));
    std::random_shuffle ( list->begin(), list->end() );
    for(int row = 0 ; row < 5 ; row++){
        for(int column = 0 ; column < 6 ; column++){
            WordCard * now = new WordCard(list->at(row*6 + column));
            QObject::connect(now,SIGNAL(active(WordCard *)),active,SLOT(process(WordCard *)));
            this->addWidget(now,row,column,1,1);

        }
    }


}
/**
 * Create table from scratch to reset
 *
 * @brief Table::restart
 */
void Table::restart(){
    create();
}
