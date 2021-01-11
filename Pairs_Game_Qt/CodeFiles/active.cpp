#include "active.h"
/**
 * It connects cooldown timers pulse to free slot.
 * Till that pulse, program is freezed and all cards are disabled.
 *
 *
 * @brief Active::Active initializes fields with default values
 * @param main
 */
Active::Active(QTimer *main)
{
    this->activeList = new std::vector<WordCard*>();
    cooldown = new QTimer();
    this->main = main;
    QObject::connect(cooldown, SIGNAL(timeout()), this, SLOT(free()) );
}

/**
 * Pushes parameter Wordcard object to its list.
 * If the lists size is smaller than 2, nothing happens, all cards all active and selectable.
 * If the list has 2 items, in other words, there are 2 active looked cards, processes the open cards.
 * First of all emits disableall signal to disable all other closed card during process.
 *
 * If two cards have same word, matching is successful and the cards colors will be set to green and coupled fields set to true
 * and activelist cleared. Emits enableall to reenable all other closed cards to open and emits score to increment score by 1.
 *
 * If two cards have different words,their colors settet to red and cooldown timer starts for 0,642 seconds. This pulse is binded
 * to the free slot which enables all other cards and reverse the active cards that are wrongly matched. This makes game stop for about half seconds and allows
 * user to see its wrong match.
 *
 * @brief Active::process
 * @param one
 */
void Active::process(WordCard *one){
    this->activeList->push_back(one);

    if(int(this->activeList->size()) == 2 ){
        emit disableAll();
        w1 = this->activeList->at(0);
        w2 = this->activeList->at(1);
        this->activeList->clear();

        if(w1->text() == w2->text()){
            w1->setColor("green");
            w2->setColor("green");
            w1->coupled = w2->coupled = true;
            emit enableAll();
            emit score();
        }
        else{
            this->cooldown->start(642);
            //main->stop();
            w1->setColor("red");
            w2->setColor("red");



        }
    }
}
/**
 * Reverses active cards and make all other cards enabled.
 *
 * @brief Active::free
 */
void Active::free(){
    this->cooldown->stop();
    w1->reverse();
    w2->reverse();
    emit enableAll();
    //main->start(1000);

}
/**
 * Clears the list
 * @brief Active::restart
 */
void Active::restart(){
    this->activeList->clear();
}
