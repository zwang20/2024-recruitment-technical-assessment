use axum::{http::StatusCode, response::IntoResponse, Json};
use serde::{Deserialize, Serialize};

pub async fn process_data(Json(request): Json<DataRequest>) -> impl IntoResponse {
    // Calculate sums and return response
    let mut response = DataResponse {
        string_len: 0,
        int_sum: 0,
    };

    for element in request.data {
        match element {
            serde_json::Value::Number(x) if x.is_i64() => response.int_sum += x.as_i64().unwrap(),
            serde_json::Value::String(s) => response.string_len += s.len(),
            _ => (),
        }
    }

    (StatusCode::OK, Json(response))
}

#[derive(Deserialize, Debug)]
pub struct DataRequest {
    // Add any fields here
    data: Vec<serde_json::Value>,
}

#[derive(Serialize)]
pub struct DataResponse {
    // Add any fields here
    string_len: usize,
    int_sum: i64,
}
