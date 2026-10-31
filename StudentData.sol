
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StudentData {

    // Structure to store student details
    struct Student {
        uint rollNo;
        string name;
        string department;
        uint marks;
    }

    // Dynamic array of students
    Student[] public students;

    // Function to add a new student
    function addStudent(
        uint _rollNo,
        string memory _name,
        string memory _department,
        uint _marks
    ) public {
        students.push(
            Student(_rollNo, _name, _department, _marks)
        );
    }

    // Function to retrieve student details using index
    function getStudent(uint _index)
        public
        view
        returns (
            uint,
            string memory,
            string memory,
            uint
        )
    {
        require(_index < students.length, "Invalid student index");

        Student memory s = students[_index];

        return (
            s.rollNo,
            s.name,
            s.department,
            s.marks
        );
    }

    // Function to get the total number of students
    function getStudentCount() public view returns (uint) {
        return students.length;
    }
}
