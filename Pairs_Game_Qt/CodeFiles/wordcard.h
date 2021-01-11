#ifndef WORDCARD_H
#define WORDCARD_H

#include <QPalette>
#include <QPushButton>

class WordCard : public QPushButton
{
    Q_OBJECT
public:
    WordCard(const QString& text, QWidget* parent=0);
    QString hiddenText;         // The real word behind the card
    QColor defaultColor;        // The default color of card
    QPalette pal;               // Palette object for wordcard
    bool act;                   // Bool value that determines that this card is active or not
    bool coupled;               // Bool value that determines this card is coupled with other card or not

    void reverse();                 // Reverses the card to its initial position and initial colour
    void setColor(QString colour);  // Set the colour of the card with respect to parameter

signals:
    void active(WordCard * one);    // When a card turned with look slot, this signal emitted to indicate that this card is active.


public slots:
    void look();    // Opens the card and its hidden text, change status act to true and emits active signal.

};

#endif // WORDCARD_H
