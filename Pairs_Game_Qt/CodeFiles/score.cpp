#include "score.h"

/**
 * @brief Score::Score initializes fields with default values
 */
Score::Score()
{

    this->score = 0;
    this->display = new QLabel("Score: " + QString::number(score));

}

/**
 * Increments score by 1
 * Emits endgame signal when score is 15. This signal catched by "Result" class which handles endgame situations
 *
 * @brief Score::scoreUp
 */
void Score::scoreUp(){
    this->score++;
    this->display->setText("Score: " + QString::number(score)) ;
    if(this->score == 15){
        emit endgame();
    }
}

/**
 * Resets fields.
 *
 * @brief Score::restart
 */
void Score::restart(){
    this->score = 0;
    this->display->setText("Score: " + QString::number(score)) ;
}
