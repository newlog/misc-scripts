use select::document::Document;
use select::predicate::Name;

pub fn get_image_links(html: &str) -> Vec<String> {
    let mut v: Vec<String> = vec![];
    let document = Document::from(html);
    for node in document.find(Name("img")).iter() {
        let link = node.attr("src").unwrap().to_owned();
        v.push(link);
    }
    v
}

pub fn get_name_from_image_link(image_link: &str) -> String {
    image_link.split("/").last().unwrap().to_owned()
}