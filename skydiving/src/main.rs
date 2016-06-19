extern crate hyper;
extern crate select;

mod utils;

fn download_images(image_links: Vec<String>) {
    let mut count = 0u32;
    for image_link in image_links {
        let image_name = utils::parse::get_name_from_image_link(&image_link);
        let mut response = utils::http::get_response(&image_link);
        let mut file = utils::file::create_file(&image_name);
        let bytes_written = utils::file::write_response_to_file(&mut file, &mut response);
        println!("{} saved. Size: {} bytes", image_name, bytes_written);
        if count ==  1 {
            break;
        }         
        count += 1;  
    }
}

fn main() {
    let html_source = utils::http::get_source("http://www.meneame.net").unwrap();
    let image_links = utils::parse::get_image_links(&html_source);
    println!("{} images found:", image_links.len());
    download_images(image_links)
}
