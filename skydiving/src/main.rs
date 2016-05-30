extern crate hyper;
extern crate select;

mod utils;

fn download_images(image_links: Vec<String>) {
    for image_link in image_links {
        println!("{}", image_link);
        let image = utils::http::get_bytes(&image_link);
        for byte in image.unwrap() {
            println!("{:?}", byte.unwrap());            
        }

    }
}

fn main() {
    let html_source = utils::http::get_source("http://www.meneame.net").unwrap();
    let image_links = utils::parse::get_image_links(&html_source);
    println!("{} images found:", image_links.len());
    download_images(image_links)
}
