use hyper;
use std::io::Read;
use hyper::{Client};
use hyper::client::response::Response;

pub fn get_source(url: &str) -> hyper::Result<String> {
    let client = Client::new();
    let mut response = try!(client.get(url).send());
    let mut buf = String::new();
    try!(response.read_to_string(&mut buf));
    Ok(buf)
}

pub fn get_response(url: &str) -> Response {
    let client = Client::new();
    match client.get(url).send() {
        Err(why) => panic!("Request to {} was not successful. Error: {}", url, why),
        Ok(response) => response,
    }
}