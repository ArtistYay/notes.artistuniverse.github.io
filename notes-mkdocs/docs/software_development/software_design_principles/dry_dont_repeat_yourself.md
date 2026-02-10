# DRY (Don’t Repeat Yourself)

## Overview

Clean your code by putting parts of it in one central place so you can make changes easily. For example, utilize functions.

## Best Practices

- Clean up duplication regularly as it creeps in.
- Keep business rules and logic in one place.
- Use shared libraries for common utilities.

!!! youtube "DRY (Don’t Repeat Yourself)"
	<iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/IGH4-ZhfVDk?si=75_-ybyL-mble9ve" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

## Real-world scenario

Got this example from [Geeks for Geeks](https://www.geeksforgeeks.org/system-design/solid-principle-in-programming-understand-with-real-life-examples/#:~:text=1%2E%20Single%20Responsibility%20Principle)

``` py linenums="1"
// Without DRY
function validateEmailFormat1(email) {
    // Validation logic
    if (email.includes("@") && email.includes(".")) {
        return true;
    } else {
        return false;
    }
}

function validateEmailFormat2(email) {
    // Validation logic
    if (email.includes("@") && email.includes(".")) {
        return true;
    } else {
        return false;
    }
}

// With DRY
function validateEmailFormat(email) {
    // Validation logic
    if (email.includes("@") && email.includes(".")) {
        return true;
    } else {
        return false;
    }
}
```
d