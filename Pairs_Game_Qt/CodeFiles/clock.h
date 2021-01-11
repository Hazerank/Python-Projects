#ifndef CLOCK_H
#define CLOCK_H
#include <QTimer>
#include <QLabel>
#include <QMessageBox>


class Clock : public QObject
{

Q_OBJECT

public:
    Clock(int time);
    QTimer *clock;          // Timer that countdowns from time value till 0
    QLabel *display;        // The label value of clock
    int count;              // The integer value of clock
    int time;               // The upper limit of countdown. The timi limit of the game. Taken as parameter.

signals:
    void endgame();         // Emitted when the time is up.


public slots:
    void ClockSlot();       // Handles the countdown. For every seconds, evaluates time.
    void restart();         // Resets corresponging values
    void stop();            // Stops timer
};

#endif // CLOCK_H
