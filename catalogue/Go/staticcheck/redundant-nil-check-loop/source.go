func (HTTPRequest *HTTPRequest) run(client *Client) ([]byte, error) {
	var err error
	values := make(url.Values)
	if HTTPRequest.Parameters != nil {
		for k, v := range HTTPRequest.Parameters {
			values.Set(k, fmt.Sprintf("%v", v))
		}
	}
}
