mod modules;
use app::library_function;


fn main() {
    println!("Hello from main!");
    modules::module1::function1();
    modules::module2::function2();
    library_function();
}

