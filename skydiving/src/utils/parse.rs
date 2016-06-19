use select::document::Document;
use select::predicate::Name;

pub fn get_image_links(html: &str) -> Vec<String> {
    let mut v: Vec<String> = vec![];
    let document = Document::from(html);
    for node in document.find(Name("img")).iter() {
        let data_type = node.attr("data-type").unwrap_or("").to_owned();
        let mut link = node.attr("data-src").unwrap_or("").to_owned();
        if !link.is_empty() && data_type == "image" {
            link = link.trim_left_matches("/").to_owned();
            if !link.starts_with("http://") && !link.starts_with("https://") {
                link = "https://skydivesandiego.mrmanifest.com/".to_owned() + &link;
            }
            if !v.contains(&link) {
                v.push(link);
            }
        }
    }
    v
}

pub fn get_name_from_image_link(image_link: &str) -> String {
    image_link.split("/").last().unwrap().to_owned()
}