#include "clock.h"

/**
 * Takes one int parameter to determine upper bound of countdown.
 * Sets fields with default values.
 * Connects timer timeouts to Clockslot.
 * I make use of Ps codes in this class a bit.
 *
 * @brief Clock::Clock  initializes fields with default values
 * @param time
 */
Clock::Clock(int time)
{

    this->time = time;
    this->count = 0;
    this->display = new QLabel("Time: " + QString::number(count));
    this->clock = new QTimer();

    QObject::connect(this->clock, SIGNAL(timeout()), this, SLOT(ClockSlot()) );

    this->clock->start(1000);

}

/**
 * Updates the value of timer for every seconds
 * When the time is up, emits endgame signal. This signal will be catched by "Result" class.
 *
 * @brief Clock::ClockSlot
 */
void Clock::ClockSlot(){
    this->count++;
    this->display->setText("Time: " + QString::number(count)) ;

    if(this->count == 180){
        clock->stop();
        emit endgame();

    }
}

/**
 * Resets counter and display values.
 *
 * @brief Clock::restart
 */
void Clock::restart(){
    this->count = 0;
    this->clock->start(1000);
    this->display->setText("Time: " + QString::number(count)) ;
}
/**
 * Stops timer.
 *
 * @brief Clock::stop
 */
void Clock::stop(){
    this->clock->stop();
}
