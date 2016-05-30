use hyper;
use std::io::Read;
use std::io::Bytes;
use hyper::{Client};
use hyper::client::response::Response;

pub fn get_source(url: &str) -> hyper::Result<String> {
    let client = Client::new();
    let mut response = try!(client.get(url).send());
    let mut buf = String::new();
    try!(response.read_to_string(&mut buf));
    Ok(buf)
}

pub fn get_bytes(url: &str) -> hyper::Result<Bytes<Response>> {
    let client = Client::new();
    let response = try!(client.get(url).send());
    Ok(response.bytes())
}

pub fn get_response(url: &str) -> hyper::Result<Response> {
    let client = Client::new();
    let response = try!(client.get(url).send());
    Ok(response)
}