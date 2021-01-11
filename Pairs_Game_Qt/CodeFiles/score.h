#ifndef SCORE_H
#define SCORE_H
#include <QLabel>



class Score : public QObject
{

Q_OBJECT

public:
    Score();
    QLabel * display;   // Label that keeps score value
    int score;          // Score value

signals:
    void endgame();     // Emitted when score is reached its max, 15 in this case

public slots:
    void scoreUp();     // Increments score by 1, controls corresponding situations, whether game is finished or not.
    void restart();     // Resets score and display
};

#endif // SCORE_H
