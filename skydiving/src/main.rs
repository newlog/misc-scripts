extern crate hyper;
extern crate select;

mod utils;

fn main() {
    let html_source = utils::http::get("http://www.meneame.net").unwrap();
    let image_links = utils::parse::get_image_links(&html_source);
    println!("{} images found:", image_links.len());
    println!("{:?}", (image_links));
}
