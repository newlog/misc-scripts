use select;
use select::document::Document;
use select::predicate::Name;

pub fn get_image_links(html: &str) -> Vec<&str> {
    let v: Vec<&str> = vec![];
    let document = Document::from(html);
    for node in document.find(Name("img")).iter() {
        //println!("{:?}", node.attr("src").unwrap());
        let link = node.attr("src").unwrap();
        v.push(link);
    }
    v
}