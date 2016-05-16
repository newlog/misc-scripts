extern crate hyper;

mod utils;

fn main() {
    println!("{:?}", utils::http::get(""));
}
