package main

import (
    "log"
    "net/http"

    "github.com/gorilla/mux"
    "gorm.io/driver/sqlite"
    "gorm.io/gorm"
    "myapp/handlers"
    "myapp/models"
)

func main() {
    // Инициализация базы данных
    db, err := gorm.Open(sqlite.Open("test.db"), &gorm.Config{})
    if err != nil {
        panic("failed to connect database")
    }

    // Миграция схемы
    db.AutoMigrate(&models.Todo{})

    // Инициализация роутера
    r := mux.NewRouter()

    // Определение маршрутов
    r.HandleFunc("/todos", handlers.GetTodos(db)).Methods("GET")
    r.HandleFunc("/todos", handlers.CreateTodo(db)).Methods("POST")
    r.HandleFunc("/todos/{id}", handlers.GetTodo(db)).Methods("GET")
    r.HandleFunc("/todos/{id}", handlers.UpdateTodo(db)).Methods("PUT")
    r.HandleFunc("/todos/{id}", handlers.DeleteTodo(db)).Methods("DELETE")

    // Запуск сервера
    log.Println("Server is running on port 8080")
    log.Fatal(http.ListenAndServe(":8080", r))
}

