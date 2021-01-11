#include "result.h"
/**
 * Connects buttons' clicked signals to its signals.
 * With this, class can emit corresponging signal correctly.
 * This signals catched from all other classes to restart game or from game object to quit game.
 *
 * @brief Result::Result initializes fields with default values
 * @param score
 */
Result::Result(Score * score)
{
    this->score = score;
    ex = new QPushButton();
    ng = new QPushButton();
    QObject::connect(ng,SIGNAL(clicked()),this, SIGNAL(newGame()));
    QObject::connect(ex,SIGNAL(clicked()),this, SIGNAL(quit()));
    ex->setText("Quit"); ng->setText("Restart");

}
/**
 * Evaluates situation. If score is smaller than 15, creates loose message, win message otherwise.
 * Shows current score and asks for quit or restart.
 * Regarding to users decision, corresponding signals are emitted.
 *
 *
 * @brief Result::evaluate
 */
void Result::evaluate(){

    emit freeze();
    if(this->score->score == 15){
        QMessageBox *res = new QMessageBox();

        res->setWindowTitle("Game Over");
        res->setText("You Won\n\nYour score: " + QString::number(this->score->score));
        res->addButton(ng, QMessageBox::AcceptRole);
        res->addButton(ex, QMessageBox::AcceptRole);


        res->exec();

    }
    else {
        QMessageBox *res = new QMessageBox();


        res->setWindowTitle("Game Over");
        res->setText("You loose\n\nYour score: " + QString::number(this->score->score));
        res->addButton(ng, QMessageBox::AcceptRole);
        res->addButton(ex, QMessageBox::AcceptRole);


        res->exec();
    }
}


