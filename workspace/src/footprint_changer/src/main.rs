use rclrs::RclrsError;
use std::sync::{Arc, Mutex};
use geometry_msgs::msg::{Polygon, Point32};
use std_msgs::msg::UInt8;

struct FootprintChanger {
    node: Arc<rclrs::Node>,
    footprint_change_required: Arc<Mutex<bool>>,
    vertex_count: Arc<Mutex<u8>>,
    _vertex_count_sub: Arc<rclrs::Subscription<UInt8>>,
    local_pub: Arc<rclrs::Publisher<Polygon>>,
    global_pub: Arc<rclrs::Publisher<Polygon>>,
}

impl FootprintChanger {
    fn new(context: &rclrs::Context) -> Result<Self, RclrsError> {
        println!("FootprintChanger node started!!");
        let node = rclrs::Node::new(context, "footprint_changer")?;
        let vertex_count = Arc::new(Mutex::new(3));
        let vertex_count_cb = Arc::clone(&vertex_count);
        let footprint_change_required = Arc::new(Mutex::new(false));
        let footprint_change_required_cb = Arc::clone(&footprint_change_required);
        let _vertex_count_sub = node.create_subscription("set_footprint_vertex_number", rclrs::QOS_PROFILE_DEFAULT, move |msg: UInt8| {
            *vertex_count_cb.lock().unwrap() = msg.data;
            *footprint_change_required_cb.lock().unwrap() = true;
        })?;
        let local_pub = node.create_publisher("local_costmap/footprint", rclrs::QOS_PROFILE_DEFAULT)?;
        let global_pub = node.create_publisher("global_costmap/footprint", rclrs::QOS_PROFILE_DEFAULT)?;
        Ok(FootprintChanger {
            node,
            footprint_change_required,
            vertex_count,
            _vertex_count_sub,
            local_pub,
            global_pub,
        })
    }

    fn update_footprint(&self) {
        let vertices = *self.vertex_count.lock().unwrap() as usize;
        if vertices < 3 {
            println!("Error: Vertex count should be greater than 2!!");
            return;
        }
        let footprint = Self::generate_polygon(vertices);
        let _  = self.local_pub.publish(footprint.clone());
        let _  = self.global_pub.publish(footprint);
    }

    fn generate_polygon(vertices: usize) -> Polygon {
        let mut poly = Polygon { points: vec![] };
        let radius = 0.2;
        let angle_step = 2.0 * std::f32::consts::PI / vertices as f32;
        for i in 0..vertices {
            let angle = i as f32 * angle_step;
            poly.points.push(Point32 {
                x: radius * angle.cos(),
                y: radius * angle.sin(),
                z: 0.0,
            });
        }
        poly
    }

    fn set_footprint_change_required_status(&self, status: bool) {
        *self.footprint_change_required.lock().unwrap() = status;
    }

    fn get_footprint_change_required_status(&self) -> bool {
        *self.footprint_change_required.lock().unwrap()
    }
}

fn main() -> Result<(), RclrsError> {
    let context = rclrs::Context::new(std::env::args())?;
    let node = Arc::new(FootprintChanger::new(&context)?);
    let pub_node = Arc::clone(&node);
    std::thread::spawn(move || {
        loop {
            use std::time::Duration;
            std::thread::sleep(Duration::from_millis(100));
            if pub_node.get_footprint_change_required_status() == true {
                println!("Update footprint!!");
                pub_node.update_footprint();
                pub_node.set_footprint_change_required_status(false);
            }
        }
    });

    let _ = rclrs::spin(Arc::clone(&node.node));
    Ok(())
}
