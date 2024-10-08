package handlers

import (
    "encoding/json"
    "net/http"
    "strconv"

    "github.com/gorilla/mux"
    "gorm.io/gorm"
    "myapp/models"
)

func GetTodos(db *gorm.DB) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        var todos []models.Todo
        db.Find(&todos)
        json.NewEncoder(w).Encode(todos)
    }
}

func CreateTodo(db *gorm.DB) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        var todo models.Todo
        json.NewDecoder(r.Body).Decode(&todo)
        db.Create(&todo)
        json.NewEncoder(w).Encode(todo)
    }
}

func GetTodo(db *gorm.DB) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        params := mux.Vars(r)
        id, _ := strconv.Atoi(params["id"])
        var todo models.Todo
        db.First(&todo, id)
        json.NewEncoder(w).Encode(todo)
    }
}

func UpdateTodo(db *gorm.DB) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        params := mux.Vars(r)
        id, _ := strconv.Atoi(params["id"])
        var todo models.Todo
        db.First(&todo, id)
        json.NewDecoder(r.Body).Decode(&todo)
        db.Save(&todo)
        json.NewEncoder(w).Encode(todo)
    }
}

func DeleteTodo(db *gorm.DB) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        params := mux.Vars(r)
        id, _ := strconv.Atoi(params["id"])
        var todo models.Todo
        db.Delete(&todo, id)
        json.NewEncoder(w).Encode("Todo deleted successfully")
    }
}

