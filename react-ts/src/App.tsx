import { useEffect, useState } from "react";
import EmployeeList from "./components/EmployeeList";

const employees = [
  {
    id: 1,
    name: "John Doe",
    
  },
];

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    async function getData() {
      const resp = await fetch(
        "https://a8303896e1.execute-api.us-east-1.amazonaws.com/prod"
      ).then((res) => res.json());

      setData(resp);
    }

    getData();
  }, []);

  return (
    <div>
      {data && <h2>{JSON.stringify(data)}</h2>}
      <EmployeeList />
    </div>
  );
}

export default App;
