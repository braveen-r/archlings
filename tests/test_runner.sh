#!/bin/bash
set -e

echo "🔨 Building base image (quiet mode)..."
docker build -t archlings-base -f docker/Dockerfile.arch-lab . > /dev/null

for DIR in scenarios/*; do
    if [ ! -d "$DIR" ]; then continue; fi
    SCENARIO=$(basename "$DIR")
    
    echo "======================================"
    echo "🧪 Testing Scenario: $SCENARIO"
    
    CONTAINER="test-$SCENARIO"
    docker rm -f "$CONTAINER" 2>/dev/null || true
    
    # Start container in the background
    docker run -d --name "$CONTAINER" -v "$(pwd)/$DIR:/lab" -w "/root" archlings-base tail -f /dev/null > /dev/null
    
    echo "💥 Injecting fault..."
    docker exec "$CONTAINER" /bin/bash /lab/setup.sh > /dev/null
    
    echo "🔍 Ensuring verify fails initially..."
    if docker exec "$CONTAINER" /bin/bash /lab/verify.sh > /dev/null 2>&1; then
        echo "❌ ERROR: Verify passed BEFORE the fix was applied!"
        docker rm -f "$CONTAINER" > /dev/null
        exit 1
    fi
    echo "✅ Verify correctly failed."
    
    echo "🛠️ Extracting and applying fix from solution.md..."
    # Extract bash code blocks from the markdown file
    sed -n '/```bash/,/```/p' "$DIR/solution.md" | grep -v '```' > temp_fix.sh
    docker cp temp_fix.sh "$CONTAINER":/root/fix.sh
    docker exec "$CONTAINER" /bin/bash /root/fix.sh > /dev/null 2>&1
    
    echo "🔍 Ensuring verify passes after fix..."
    if docker exec "$CONTAINER" /bin/bash /lab/verify.sh > /dev/null 2>&1; then
        echo "✅ Verify correctly passed!"
    else
        echo "❌ ERROR: Verify failed AFTER the solution was applied!"
        docker rm -f "$CONTAINER" > /dev/null
        exit 1
    fi
    
    docker rm -f "$CONTAINER" > /dev/null
    rm temp_fix.sh
done

echo "======================================"
echo "🎉 ALL SCENARIOS PASSED VALIDATION!"
