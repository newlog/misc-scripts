use hyper::client::response::Response;
use std::path::Path;
use std::fs::File;
use std::io::copy;

pub fn create_file(name: &str) -> File {
    let filename_str = "/tmp/skydive/".to_string() + name;
    let filename = Path::new(&filename_str);
    match File::create(&filename) {
        Err(why) => panic!("File could not be created {}. Error: {}", filename.display(), why),
        Ok(file) => file,
    }
}

pub fn write_response_to_file(file: &mut File, response: &mut Response) -> u64 {
    match copy(response, file) {
        Err(why) => panic!("File could not be written. Error: {}", why),
        Ok(bytes_written) => bytes_written,
    }
}