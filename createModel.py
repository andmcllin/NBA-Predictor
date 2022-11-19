import pandas as pd
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical
from keras.callbacks import ModelCheckpoint, EarlyStopping

df = pd.read_csv('gameResultsandZScoreDiff.csv')

X = df.drop(columns=['Date', 'Visiting Team', 'Home Team', 'Home Win'], axis=1)
y = to_categorical(df['Home Win'])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=47)

n_cols = X_train.shape[1]

model = Sequential()

model.add(Dense(17, activation='relu', input_shape=(n_cols,)))
model.add(Dense(17, activation='relu'))
model.add(Dense(17, activation='relu'))
model.add(Dense(17, activation='relu'))
model.add(Dense(17, activation='relu'))

model.add(Dense(2, activation='softmax'))

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

callbacks = [
    ModelCheckpoint('NBAPredictor.h5', save_best_only=True, verbose=0),
    EarlyStopping(patience=3, monitor='val_loss', verbose=1)
    ]

model.fit(X_train, y_train, epochs=100, validation_split=0.2, callbacks=callbacks)