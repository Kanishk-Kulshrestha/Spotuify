#include <ncurses.h>
#include <bits/stdc++.h>
using namespace std;

int main(){
	initscr();
	WINDOW *win = newwin(15,17,2,10);
	refresh();

	box(win, 0, 0);

	mvwprintw(win, 0, 1, "Greeter");
	mvwprintw(win, 1, 1, "Hello");

	wrefresh(win);

	string s;
	scanf("%s", &s);
	endwin();
	return 0;
}

