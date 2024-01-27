import { useEffect, useState } from "react";
import EmployeeList from "./components/EmployeeList";

// const employees = [
//   {
//     id: 1,
//     name: "John Doe",
//   },
// ];
// n=12 pilots total
// shifts: D, E, N, D/E; day, evening, night, day/evening
// Pilots per shift:
// Day: 1-2
// Evening: 1-2 (prefer 2)
// Night: 1
// Day/Evening: 1
// d/e shifts are rare: make it manual.

// max shifts per month: 14 shifts per pilot offered to each pilot, will be 13 next year
// "all pilots must be scheduled 14 days a month"
// pilots cannot work more than 5 days in a row
// if a pilot works the night shift they cannot work the following day shift.

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
