letter = readtable("alejandro-99\alejandro-99-A.txt");
% letter.X = letter.X*1.5; % Aspect ratio 1:1
letter.Time = (letter.Time - letter.Time(1))/1000;
plot(letter.X,letter.Y)
axis equal

dur = letter.Time(end)
aratio = range(letter.Y)/range(letter.X)
