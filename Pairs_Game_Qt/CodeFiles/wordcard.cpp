#include "wordcard.h"

/**
 * Sends parameters to QPushButton via calling it.
 * Connects clicked signal to look slot indicates that when clicked, card would be looked
 *
 * I make use of Ps codes in this class a bit.
 * @brief WordCard::WordCard initializes fields with default values
 * @param text
 * @param parent
 */
WordCard::WordCard(const QString& text, QWidget* parent): QPushButton((text,parent))
{
    act = true;
    coupled = false;
    this->hiddenText = text;
    this->setText("---");
    this->defaultColor = Qt::lightGray;
    pal = palette();
    pal.setColor(QPalette::Button , defaultColor);
    setPalette(pal);
    update();
    setAutoFillBackground(true);
    QObject::connect(this,SIGNAL(clicked()),this,SLOT(look()));

}

/**
 * In order to do something, card should active and not coupled.
 * This control prevent reopen same card or open the cards that are coupled.
 *
 * Changes the hidden text and "---" values, reveals the hidden text.
 * Act value changes to false which makes this card active
 * Emits active signal with itself as parameter. This signal will be catched by "Active" class which handles active card situations.
 *
 * @brief WordCard::look
 */
void WordCard::look(){
    if(act && !coupled){
        QString temp = this->text();
        this->setText(this->hiddenText);
        this->hiddenText = temp;
        act = false;
        emit active(this);
    }
}

/**
 * Returns card to its initial value.
 * This happens after an unsuccesfull coupling try.
 *
 *
 * @brief WordCard::reverse
 */
void WordCard::reverse(){

    QString temp = this->text();
    this->setText(this->hiddenText);
    this->hiddenText = temp;
    act = true;
    pal.setColor(QPalette::Button , defaultColor);
    setPalette(pal);
    update();

}

/**
 * Changes the colour of card with respect to parameter.
 *
 * @brief WordCard::setColor
 * @param colour The color value which can be red or green, in other cases, interpreted as default colour.
 */
void WordCard::setColor(QString colour){

    if(colour == "red"){
        pal.setColor(QPalette::Button , Qt::red);
    }
    else if(colour == "green"){
        pal.setColor(QPalette::Button , Qt::green);
    }
    else{
        pal.setColor(QPalette::Button , defaultColor);
    }
    setPalette(pal);
    update();

}
