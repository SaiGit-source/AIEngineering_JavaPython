package com.vectordb.demo.RAG;

import org.springframework.ai.document.Document;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
public class productsController {
    @Autowired
    private VectorStore vectorStore;

    // we send requests to get (list of) products related to the keyword
    @GetMapping("/api/products")
    public List<Document> getProducts(@RequestParam String text){
        return vectorStore.similaritySearch(text); // similaritySearch(text) will give you List<Document> matching with this text but we have to return a String
    }
}


// i requested all products related to only "tea"
// problem is, it breaks the text into documents in the way it wants. sometimes by Title, sometimes by Description. How do we customize it?
/*
 GET http://localhost:8080/api/products?text=tea

[
    {
        "id": "35488864-265b-42b2-a8c4-e12964857bbf",
        "text": "Price: $9.99\r\nCategory: Herbal Tea\r\nFeatures: Caffeine-free, Calming effect, Natural herbs, Individually wrapped bags\r\n\r\nTitle: \"Electric Tea Kettle\"\r\nDescription: Fast-boil electric kettle with temperature control for different types of tea.\r\nPrice: $49.99\r\nCategory: Kitchen Appliances\r\nFeatures: Temperature presets, Stainless steel, Auto shut-off, 1.7L capacity\r\n\r\nTitle: \"Tea Infuser Stainless Steel\"\r\nDescription: Reusable stainless steel tea infuser for brewing loose leaf tea effortlessly.\r\nPrice: $6.99\r\nCategory: Tea Accessories\r\nFeatures: Fine mesh filter, Reusable, Easy to clean, Fits most cups",
        "media": null,
        "metadata": {
            "chunk_index": 1,
            "charset": "UTF-8",
            "parent_document_id": "bd5227c6-f0c6-475a-a7c1-84e8a981531f",
            "source": "product_details.txt",
            "distance": 0.5826906162954104,
            "total_chunks": 2
        },
        "score": 0.41730938370458953
    },
    {
        "id": "cbf334e1-28a3-4780-985c-2344e30d6a29",
        "text": "Title: \"Smart Fitness Watch\"\r\nDescription: Waterproof fitness smartwatch with heart rate monitoring, sleep tracking, and GPS support.\r\nPrice: $79.99\r\nCategory: Wearables\r\nFeatures: Heart rate sensor, GPS, Sleep tracking, 7-day battery life\r\n\r\nTitle: \"Portable Power Bank 20000mAh\"\r\nDescription: High-capacity power bank with fast charging and dual USB output for multiple devices.\r\nPrice: $39.99\r\nCategory: Electronics\r\nFeatures: Fast charging, Dual USB ports, LED indicator, Compact design\r\n\r\nTitle: \"Noise Cancelling Over-Ear Headphones\"\r\nDescription: Over-ear headphones with active noise cancellation and immersive surround sound.\r\nPrice: $129.99\r\nCategory: Audio\r\nFeatures: Active noise cancellation, Bluetooth 5.2, Foldable design, 40-hour battery\r\n\r\nTitle: \"Ergonomic Office Chair\"\r\nDescription: Adjustable ergonomic office chair designed for long working hours and proper posture.\r\nPrice: $219.99\r\nCategory: Furniture\r\nFeatures: Lumbar support, Adjustable height, Breathable mesh, 360° swivel\r\n\r\nTitle: \"Wireless Mechanical Keyboard\"\r\nDescription: Compact mechanical keyboard with customizable RGB lighting and wireless connectivity.\r\nPrice: $89.99\r\nCategory: Computer Accessories\r\nFeatures: RGB backlighting, Bluetooth & USB-C, Mechanical switches, Anti-ghosting\r\n\r\nTitle: \"4K Ultra HD Action Camera\"\r\nDescription: Rugged action camera capable of recording 4K videos with image stabilization.\r\nPrice: $149.99\r\nCategory: Cameras\r\nFeatures: 4K recording, Image stabilization, Waterproof casing, Wi-Fi enabled\r\n\r\nTitle: \"Smart Home Wi-Fi Plug\"\r\nDescription: Smart plug that lets you control appliances remotely using a mobile app or voice assistant.\r\nPrice: $19.99\r\nCategory: Smart Home\r\nFeatures: Voice control, Mobile app support, Energy monitoring, Scheduling\r\n\r\nTitle: \"USB-C Hub Multiport Adapter\"\r\nDescription: Versatile USB-C hub expanding one port into multiple connections for laptops and tablets.\r\nPrice: $34.99\r\nCategory: Computer Accessories\r\nFeatures: HDMI output, USB 3.0 ports, SD card reader, Power delivery\r\n\r\nTitle: \"Electric Coffee Grinder\"\r\nDescription: Compact coffee grinder with stainless steel blades for fresh-ground coffee beans.\r\nPrice: $29.99\r\nCategory: Kitchen Appliances\r\nFeatures: Stainless steel blades, One-touch operation, Compact size, Easy to clean\r\n\r\nTitle: \"Smart LED Desk Lamp\"\r\nDescription: Adjustable LED desk lamp with multiple brightness levels and color temperature control.\r\nPrice: $44.99\r\nCategory: Home & Office\r\nFeatures: Touch controls, Adjustable arm, Eye-care lighting, USB charging port\r\n\r\nTitle: \"Wireless Charging Stand\"\r\nDescription: Fast wireless charging stand compatible with phones, earbuds, and smartwatches.\r\nPrice: $27.99\r\nCategory: Electronics\r\nFeatures: Fast wireless charging, Anti-slip base, LED indicator, Multi-device support\r\n\r\nTitle: \"Smart Doorbell Camera\"\r\nDescription: Wi-Fi enabled doorbell camera with motion detection and two-way audio.\r\nPrice: $99.99\r\nCategory: Smart Home\r\nFeatures: HD video, Night vision, Motion alerts, Two-way audio\r\n\r\nTitle: \"Glass Teapot with Infuser\"\r\nDescription: Heat-resistant glass teapot with removable infuser for loose leaf tea.\r\nPrice: $27.99\r\nCategory: Tea Accessories\r\nFeatures: Borosilicate glass, Removable infuser, Drip-free spout, 800ml capacity\r\n\r\nTitle: \"Cold Brew Tea Pitcher\"\r\nDescription: Cold brew pitcher designed for smooth, refreshing iced tea at home.\r\nPrice: $22.99\r\nCategory: Drinkware\r\nFeatures: BPA-free, Fine mesh filter, Leak-proof lid, Easy to store\r\n\r\nTitle: \"Herbal Chamomile Tea\"\r\nDescription: Caffeine-free chamomile herbal tea ideal for relaxation and better sleep.",
        "media": null,
        "metadata": {
            "chunk_index": 0,
            "charset": "UTF-8",
            "parent_document_id": "bd5227c6-f0c6-475a-a7c1-84e8a981531f",
            "source": "product_details.txt",
            "distance": 0.7043641243306213,
            "total_chunks": 2
        },
        "score": 0.2956358756693786
    }
]
*/