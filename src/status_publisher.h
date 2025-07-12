// status_publisher.h
#ifndef STATUS_PUBLISHER_H
#define STATUS_PUBLISHER_H
void status_publisher_init(void);
void status_publisher_send(const char *json);
#endif